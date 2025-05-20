#pragma once
#include <string>
#include <eigen/Eigen/Sparse>
#include "../Chemical/Chemical.hpp"

using Vec = Eigen::VectorXd;
using SpMat = Eigen::SparseMatrix<double>;

class FDM
{
	public:
		void get_s_chem(Vec&, int);
		void print_points(std::string&);
		void print_etch2D(
			std::string&, int, int,
			double, double, double, double, double);
		void print_etch2D_probe_elec_gamma(
			std::string&, int, int,
			double, double, double, double, double);
		explicit FDM(std::string&, Chemical&);
	private:
		double const Lx = 1e-1; // 100 mm
		double const Ly = 1e-3; // 1 mm
		int nx, ny, n2d, n3d;
		Chemical& Chem;
		Vec x, y, vx, b0, u,
		    blap, bgradx, bgrady, bd, ba;
		SpMat A, Alap, Agradx, Agrady, Ad, Aa;

		void init_vx(double);
		void init_u();
		void init_prob(double, double, double);
		double get_sleft(int, int);
		double get_sright(int, int);
		void get_f_chem(Vec&);
		void get_J_chem(SpMat&);
		int solve_etch2D(
			int, int, double, double, double, double, double);
		int solve_LM(int, double, double, double, double, double, double);
		int solve_NR(int, double, double, double, double);
		void write_etch2D(std::string&);
};
