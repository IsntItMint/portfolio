#pragma once
#include <eigen/Eigen/Sparse>
#include "../Chemical/Chemical.hpp"

using Vec = Eigen::VectorXd;
using SpMat = Eigen::SparseMatrix<double>;
using T = Eigen::Triplet<double>;
using vecT = std::vector<T>;

class FDM_maker
{
	public:
		explicit FDM_maker(int, int, double, double, double, double, double, Chemical&);
		void get_lap(SpMat&, Vec&);
		void get_gradx(SpMat&, Vec&);
		void get_grady(SpMat&, Vec&);
	private:
		int nx, ny, n2d, n3d;
		double ks, dxi, deta, pxi, peta, p2xi, p2eta;
		Chemical& Chem;
		Vec ax, ay, bL, bR, bD, bU;
		SpMat AL, AR, AD, AU;

		void get_OmegaL(SpMat&);
		void get_OmegaR(SpMat&);
		void get_OmegaD(SpMat&);
		void get_OmegaU(SpMat&);
		void get_GammaL(SpMat&);
		void get_GammaR(SpMat&);
		void get_GammaD(SpMat&);
		void get_GammaU(SpMat&);
		void get_L();
		void get_R();
		void get_D();
		void get_U();
};
