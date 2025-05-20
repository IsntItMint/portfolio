#include "FDM.hpp"

int FDM::solve_etch2D(int maxitr_LM, int maxitr_NR, double lmd0, double nu, double chem_gamma, double elec_gamma, double difu_gamma)
{
	int result;
	// result = solve_LM(maxitr_LM, 1.0, lmd0, nu, chem_gamma, 0.0);
	// result = solve_NR(maxitr_NR, 1e-14, chem_gamma, 0.0);

	result = solve_NR(2, 1e-14, chem_gamma, elec_gamma, difu_gamma);
	result = solve_LM(maxitr_LM, 1e-14, lmd0, nu, chem_gamma, elec_gamma, difu_gamma);
	result = solve_NR(maxitr_NR, 1e-14, chem_gamma, elec_gamma, difu_gamma);
	return result;
}
