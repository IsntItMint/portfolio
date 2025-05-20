#include <omp.h>
#include "FDM_maker.hpp"

void FDM_maker::get_OmegaL(SpMat& A)
{
	vecT triplets;
	triplets.reserve(n3d);
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(n3d/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int idx = 0; idx < n3d; ++idx)
		{
			int i = idx % nx;
			if (i == 0)
			{
				continue;
			}
			triplets_i.emplace_back(idx, idx-1, 1.0);
		}
		#pragma omp critical
		{
			triplets.insert(triplets.end(), triplets_i.begin(), triplets_i.end());
		}
	}
	A.setFromTriplets(triplets.begin(), triplets.end());
}

void FDM_maker::get_OmegaR(SpMat& A)
{
	vecT triplets;
	triplets.reserve(n3d);
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(n3d/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int idx = 0; idx < n3d; ++idx)
		{
			int i = idx % nx;
			if (i == nx-1)
			{
				continue;
			}
			triplets_i.emplace_back(idx, idx+1, 1.0);
		}
		#pragma omp critical
		{
			triplets.insert(triplets.end(), triplets_i.begin(), triplets_i.end());
		}
	}
	A.setFromTriplets(triplets.begin(), triplets.end());
}

void FDM_maker::get_OmegaD(SpMat& A)
{
	vecT triplets;
	triplets.reserve(n3d);
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(n3d/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int idx = 0; idx < n3d; ++idx)
		{
			int j = (idx / nx) % ny;
			if (j == 0)
			{
				continue;
			}
			triplets_i.emplace_back(idx, idx-nx, 1.0);
		}
		#pragma omp critical
		{
			triplets.insert(triplets.end(), triplets_i.begin(), triplets_i.end());
		}
	}
	A.setFromTriplets(triplets.begin(), triplets.end());
}

void FDM_maker::get_OmegaU(SpMat& A)
{
	vecT triplets;
	triplets.reserve(n3d);
	#pragma omp parallel
	{
		vecT triplets_i;
		triplets_i.reserve(n3d/omp_get_num_threads());
		#pragma omp for simd nowait
		for (int idx = 0; idx < n3d; ++idx)
		{
			int j = (idx / nx) % ny;
			if (j == ny-1)
			{
				continue;
			}
			triplets_i.emplace_back(idx, idx+nx, 1.0);
		}
		#pragma omp critical
		{
			triplets.insert(triplets.end(), triplets_i.begin(), triplets_i.end());
		}
	}
	A.setFromTriplets(triplets.begin(), triplets.end());
}
