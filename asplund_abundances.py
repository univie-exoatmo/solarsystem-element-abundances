import numpy as np
import polars as pl
import sys

# So it turns out that there is a newer paper (Asplund et al., 2021),
# which might account for some correction towards the formation period
# of the Sun


def main():
    # Transform Table 1 to number density ratios
    a09_table1 = read_abundance_table("asplund2009/asplund2009_table1.csv")
    a09_abundances = transform_abundances(a09_table1)

    # Save that table for future use
    a09_abundances.write_csv(
        "asplund2009_abundances.csv", separator=",", null_value="-"
    )

    # Assert that, if arguments are given, there need to be two
    arguments = sys.argv
    if len(arguments) == 3:
        _, _, _ = calculate_element_ratio(
            a09_abundances, arguments[1], arguments[2]
        )


def read_abundance_table(filename: str) -> pl.DataFrame:
    """Read the digitalised Table 1 from Asplund et al. (2009)"""
    # Add "-" as null-value, so all tables are read as f64
    table = pl.read_csv(filename, comment_prefix="#", null_values=["-"])

    return table


def transform_abundances(table: pl.DataFrame) -> pl.DataFrame:
    """
    Translate the 'weird' abundance values to more usable ones. As described
    in Asplund et al. (2009), the abundances in Table 1 are given as

                X = log_10(N_X / N_H) + 12,

    where N_X and N_H are the number densities of element X and hydrogen. If
    we want to transform this to X / H, we just transform the equation to

                A = N_X / N_H = 10 ** (X - 12),

    where we can propagate the error on X using Gaussian error propagation and
    the derivate

                dA / dX = ln(10) * 10 ** (X - 12)
    """
    # Calculate number density ratios and associated errors
    x_to_h = 10 ** (table["alpha_phot"] - 12.0)
    x_to_h_err = np.sqrt(
        (np.log(10) * x_to_h) ** 2 * table["alpha_phot_err"] ** 2
    )

    # Add to the table
    ext_table = table.with_columns([
        (x_to_h).alias("x_to_H"),
        (x_to_h_err).alias("x_to_H_err")
    ])

    # Select relevant columns
    rel_table = ext_table.select(["Z", "element", "x_to_H", "x_to_H_err"])

    return rel_table


def calculate_element_ratio(
        total_table: pl.DataFrame,
        element_num: str, element_denom: str
        ) -> tuple:
    """
    Simple function to calculate the element number density ratio and
    propagation of uncertainty
    """
    # I am filling the missing values with float(0); this makes
    # calculations further on a bit more reliant, but keep in mind that 
    # this is only a work-around
    table = total_table.fill_null(0)

    id_str = f"{element_num}/{element_denom}"

    element_top = table.filter(pl.col("element") == element_num)
    element_bot = table.filter(pl.col("element") == element_denom)

    # Direct element ratio
    ratio = element_top["x_to_H"] / element_bot["x_to_H"]

    # Propagation of uncertainty
    ratio_error = np.sqrt(
        (1 / element_bot["x_to_H"]) ** 2 * element_top["x_to_H_err"] ** 2 +
        (- element_top["x_to_H"] / element_bot["x_to_H"] ** 2) ** 2 *
        element_bot["x_to_H_err"] ** 2
    )

    # Print ratio and error
    print(f"{id_str} = {ratio.item():.2f} +/- {ratio_error.item():.2f}")

    # Collapsing the results into single floats with item()
    return id_str, ratio.item(), ratio_error.item()


if __name__ == "__main__":
    main()
