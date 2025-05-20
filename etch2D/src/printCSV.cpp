#include <iostream>
#include <fstream>
#include <string>
#include "FDM/FDM.hpp"
#include "FDM_elec/FDM_elec.hpp"

void openAndCheck(std::ofstream& outfile, std::string& filename)
{
	outfile.open(filename, std::ios::trunc);
	if (!outfile.is_open())
	{
		std::cerr << filename << " open failed." << std::endl;
		return;
	}
}

void Chemical::print_chem(std::string& datadir)
{
	std::string data = datadir + "/elem.csv";
	std::ofstream outfile;
	openAndCheck(outfile, data);

	outfile << name[0];
	for (int i = 1; i < n_chem; ++i)
	{
		outfile << ',' << name[i];
	}
	outfile << std::endl;

	outfile.close();
}

void write_vector(std::ofstream& outfile, Vec& v, int start, int len)
{
	outfile << v(start);
	for (int i = start + 1; i < start + len; ++i)
	{
		outfile << ',' << v(i);
	}
	outfile << std::endl;
}

void FDM::print_points(std::string& datadir)
{
	std::string data = datadir + "/x.csv";
	std::ofstream outfile;
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, x, 0, nx);
	outfile.close();

	data = datadir + "/y.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, y, 0, ny);
	outfile.close();
}

void FDM::write_etch2D(std::string& datadir)
{
	std::string data = datadir + "/C.csv";
	std::ofstream outfile;
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, u, 0, n3d);
	outfile.close();

	data = datadir + "/s.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	Vec s = Vec::Zero(n2d);
	for (int l = 0; l < Chem.n_reac; ++l)
	{
		get_s_chem(s, l);
		write_vector(outfile, s, 0, n2d);
	}
	outfile.close();

	FDM_elec myFDM_elec(u, n2d, n3d, Chem,
		Alap, Agradx, Agrady,
		blap, bgradx, bgrady);
	data = datadir + "/p.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, myFDM_elec.px, 0, n2d);
	write_vector(outfile, myFDM_elec.py, 0, n2d);
	outfile.close();

	Vec f = Ad*u - bd;
	data = datadir + "/diffusion.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, f, 0, n3d);
	outfile.close();

	f = Aa*u - ba;
	data = datadir + "/advection.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, f, 0, n3d);
	outfile.close();

	myFDM_elec.get_f_elec(f);
	data = datadir + "/migration.csv";
	openAndCheck(outfile, data);
	outfile.precision(8);
	write_vector(outfile, f, 0, n3d);
	outfile.close();
}

void FDM::print_etch2D(
	std::string& datadir, int maxitr_LM, int maxitr_NR,
	double lmd0, double nu, double chem_gamma, double elec_gamma, double difu_gamma)
{
	solve_etch2D(maxitr_LM, maxitr_NR, lmd0, nu, chem_gamma, elec_gamma, difu_gamma);

	write_etch2D(datadir);
}

void FDM::print_etch2D_probe_elec_gamma(
	std::string& datadir, int maxitr_LM, int maxitr_NR,
	double lmd0, double nu, double chem_gamma, double elec_gamma, double difu_gamma)
{
	Vec old_u(n3d);
	double mitigation, elec_gamma2;
	mitigation = 1.0 - elec_gamma;
	for (int i = 1; i < 10; ++i)
	{
		old_u = u;
		elec_gamma2 = 1.0 - mitigation;
		int result = solve_etch2D(maxitr_LM, maxitr_NR, lmd0, nu, chem_gamma, elec_gamma2, difu_gamma);
		if (result == 1)
		{
			u = old_u;
			mitigation *= 10.0;
			break;
		}
		mitigation *= 0.1;
	}
	std::cout << "elec_mitigation = " << mitigation << std::endl;

	write_etch2D(datadir);
}
