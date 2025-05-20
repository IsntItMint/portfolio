#include <omp.h>
#include "../FDM_maker.hpp"

void FDM_maker::get_GammaR(SpMat& A)
{
	vecT triplets;
	int estimated = 2*Chem.n_chem*ny;
	triplets.reserve(estimated);

	int const i = nx-1;
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(estimated/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int j = 0; j < ny; ++j)
		{
			for (int k = 0; k < Chem.n_chem; ++k)
			{
				int idx = k*n2d + j*nx + i;
				triplets_i.emplace_back(idx, idx, 1.0);
			}
		}
		#pragma omp critical
		{
			triplets.insert(triplets.end(), triplets_i.begin(), triplets_i.end());
		}
	}
	A.setFromTriplets(triplets.begin(), triplets.end());
}
