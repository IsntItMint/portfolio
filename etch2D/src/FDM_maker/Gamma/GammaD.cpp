#include <omp.h>
#include "../FDM_maker.hpp"

void FDM_maker::get_GammaD(SpMat& A)
{
	vecT triplets;
	int estimated = 2*Chem.n_chem*ny;
	triplets.reserve(estimated);

	int const j = 0;
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(estimated/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int i = 0; i < nx; ++i)
		{
			int idx = j*nx + i;
			double v = 1.0 - ks/Chem.D[0]*deta/ay(j);
			triplets_i.emplace_back(idx, idx, v);

			idx = n2d + j*nx + i;
			if (ks >= 0)
			{
				v = ks/2/Chem.D[1]*deta/ay(j);
			}
			else
			{
				v = -Chem.D[0]/2/Chem.D[1];
			}
			triplets_i.emplace_back(idx, idx-n2d, v);
			triplets_i.emplace_back(idx, idx, 1.0);

			for (int k = 2; k < Chem.n_chem; ++k)
			{
				idx = k*n2d + j*nx + i;
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
