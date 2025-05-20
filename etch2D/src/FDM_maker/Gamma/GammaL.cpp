#include <omp.h>
#include "../FDM_maker.hpp"

void FDM_maker::get_GammaL(SpMat& A)
{
	int const i = 0;
	#pragma omp parallel for simd
	for (int j = 0; j < ny; ++j)
	{
		for (int k = 0; k < Chem.n_chem; ++k)
		{
			int idx = k*n2d + j*nx + i;
			bL(idx) = -Chem.C0[k];
		}
	}
}
