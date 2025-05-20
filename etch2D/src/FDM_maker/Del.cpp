#include <omp.h>
#include "FDM_maker.hpp"

void FDM_maker::get_lap(SpMat& A, Vec& b)
{
	int i, j, idx;
	double v;
	Vec g = Vec::Zero(n3d);
	SpMat G(n3d, n3d);

	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		i = idx % nx;
		j = (idx / nx) % ny;
		v = -2*(ax(i)*ax(i)*p2xi + ay(j)*ay(j)*p2eta);
		g(idx) = v;
	}
	A = SpMat(g.asDiagonal());

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		i = idx % nx;
		v = ax(i)*ax(i)*(p2xi + pxi);
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AL;
	b = G*bL;

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		i = idx % nx;
		v = ax(i)*ax(i)*(p2xi - pxi);
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AR;
	b += G*bR;

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		j = (idx / nx) % ny;
		v = ay(j)*ay(j)*(p2eta + peta);
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AD;
	b += G*bD;

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		j = (idx / nx) % ny;
		v = ay(j)*ay(j)*(p2eta - peta);
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AU;
	b += G*bU;

	A.prune(0.0);
	A.makeCompressed();
}

void FDM_maker::get_gradx(SpMat& A, Vec& b)
{
	int i, idx;
	double v;
	Vec g = Vec::Zero(n3d);
	SpMat G(n3d, n3d);

	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		i = idx % nx;
		v = -ax(i)*pxi;
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A = G*AL;
	b = G*bL;

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		i = idx % nx;
		v = ax(i)*pxi;
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AR;
	b += G*bR;

	A.prune(0.0);
	A.makeCompressed();
}

void FDM_maker::get_grady(SpMat& A, Vec& b)
{
	int j, idx;
	double v;
	Vec g = Vec::Zero(n3d);
	SpMat G(n3d, n3d);

	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		j = (idx / nx) % ny;
		v = -ay(j)*peta;
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A = G*AD;
	b = G*bD;

	g = Vec::Zero(n3d);
	G = SpMat(n3d, n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		j = (idx / nx) % ny;
		v = ay(j)*peta;
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	A += G*AU;
	b += G*bU;

	A.prune(0.0);
	A.makeCompressed();
}
