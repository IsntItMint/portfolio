#include <iostream>
#include <fstream>
#include <sstream>
#include <cmath>
#include <omp.h>
#include "../FDM_maker/FDM_maker.hpp"
#include "FDM.hpp"

using Vec = Eigen::VectorXd;
using SpMat = Eigen::SparseMatrix<double>;

void read_discrete(std::string& discretefile, int& nx, int& ny, double& ks, double& vavg, double& xie, double& etae)
{
	std::ifstream myfile(discretefile);
	std::string line;
	std::string element;

	if (!myfile.is_open()) {
		std::cerr << "error while opening file " << discretefile << '\n';
		return;
	}

	std::getline(myfile, line);
	
	std::getline(myfile, line);

	std::stringstream mystring(line);

	std::getline(mystring, element, ',');
	nx = std::stoi(element);

	std::getline(mystring, element, ',');
	ny = std::stoi(element);

	std::getline(mystring, element, ',');
	ks = std::stod(element);

	std::getline(mystring, element, ',');
	vavg = std::stod(element);

	std::getline(mystring, element, ',');
	xie = std::stod(element);

	std::getline(mystring, element, ',');
	etae = std::stod(element);

	mystring.clear();
	myfile.close();
}

void initmesh(Vec& x, int nx, double Lx, double xie)
{
	double Ax, dxi;
	Ax = Lx/(std::exp(xie)-1); dxi = xie/(nx-1);

	double v;
	#pragma omp parallel for simd
	for (int i = 0; i < nx; ++i)
	{
		v = Ax*(std::exp(dxi*i)-1.0);
		x(i) = v;
	}
}

FDM::FDM(std::string& discretefile, Chemical& pChem):
	Chem(pChem)
{
	double ks, vavg, xie, etae;
	read_discrete(discretefile, nx, ny, ks, vavg, xie, etae);

	n2d = nx*ny;
	n3d = Chem.n_chem*nx*ny;

	x = Vec(nx);
	initmesh(x, nx, Lx, xie);

	y = Vec(ny);
	initmesh(y, ny, Ly, etae);

	vx = Vec(ny);
	init_vx(vavg);

	u = Vec::Zero(n3d);
	init_u();

	A = SpMat(n3d, n3d);
	b0 = Vec::Zero(n3d);
	Ad = SpMat(n3d, n3d);
	bd = Vec::Zero(n3d);
	Aa = SpMat(n3d, n3d);
	ba = Vec::Zero(n3d);
	init_prob(ks, xie, etae);
}

void FDM::init_vx(double vavg)
{
	double r;
	#pragma omp parallel for simd
	for (int i = 0; i < ny; ++i)
	{
		r = y(i)/Ly;
		vx(i) = 6.0*vavg*r*(1.0-r);
	}
}

void FDM::init_u()
{
	#pragma omp parallel for simd
	for (int idx = 0; idx < n3d; ++idx)
	{
		int k = idx / n2d;
		u(idx) = Chem.C0[k];
	}
}

void FDM::init_prob(double ks, double xie, double etae)
{
	int j, k, idx;
	double v;
	FDM_maker myFDM_maker(nx, ny, Lx, Ly, xie, etae, ks, Chem);
	
	myFDM_maker.get_lap(Alap, blap);
	myFDM_maker.get_gradx(Agradx, bgradx);
	myFDM_maker.get_grady(Agrady, bgrady);

	Vec g = Vec::Zero(n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		k = idx / n2d;
		v = Chem.D[k];
		g(idx) = v;
	}
	SpMat G(n3d, n3d);
	G = SpMat(g.asDiagonal());
	Ad = G*Alap;
	Ad.prune(0.0);
	Ad.makeCompressed();
	bd = G*blap;

	g = Vec::Zero(n3d);
	#pragma omp parallel for simd
	for (idx = 0; idx < n3d; ++idx)
	{
		j = (idx / nx) % ny;
		v = -vx(j);
		g(idx) = v;
	}
	G = SpMat(g.asDiagonal());
	Aa = G*Agradx;
	Aa.prune(0.0);
	Aa.makeCompressed();
	ba = G*bgradx;

	// A = Ad + Aa;
	// A.prune(0.0);
	// A.makeCompressed();
	// b0 = ba + bd;
}
