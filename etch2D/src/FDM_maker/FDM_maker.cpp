#include <cmath>
#include <omp.h>
#include "FDM_maker.hpp"

void get_ax(Vec& ax, int nx, double Lx, double xie)
{
	double Ax, dxi;
	Ax = Lx/(std::exp(xie)-1); dxi = xie/(nx-1);

	double v;
	#pragma omp parallel for simd
	for (int i = 0; i < nx; ++i)
	{
		v = Ax*(std::exp(dxi*i)-1.0);
		ax(i) = 1.0/(v+Ax);
	}
}

FDM_maker::FDM_maker(int pnx, int pny, double pLx, double pLy,
	double xie, double etae, double pks, Chemical& pChem):
	nx(pnx), ny(pny), ks(pks), Chem(pChem)
{
	n2d = pnx*pny;
	n3d = pChem.n_chem*pnx*pny;

	dxi = xie/(nx-1); deta = etae/(ny-1);
	pxi = 1.0/2.0/dxi; peta = 1.0/2.0/deta;
	p2xi = 1.0/dxi/dxi; p2eta = 1.0/deta/deta;

	ax = Vec(pnx);
	get_ax(ax, pnx, pLx, xie);

	ay = Vec(pny);
	get_ax(ay, pny, pLy, etae);

	AL = SpMat(n3d, n3d);
	bL = Vec::Zero(n3d);
	get_L();

	AR = SpMat(n3d, n3d);
	bR = Vec::Zero(n3d);
	get_R();

	AD = SpMat(n3d, n3d);
	bD = Vec::Zero(n3d);
	get_D();

	AU = SpMat(n3d, n3d);
	bU = Vec::Zero(n3d);
	get_U();
}
