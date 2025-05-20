#include <chrono>
#include <iostream>
#include <string>
#include <filesystem>
#include "FDM/FDM.hpp"
#include "readCSV/readCSV.hpp"

using str = std::string;

int main()
{
	using std::chrono::high_resolution_clock;
	using std::chrono::duration;

	#pragma omp parallel
	{
		#pragma omp single
		std::cout << "Cores:" << omp_get_num_threads() << std::endl;
	}
	std::vector<str> inputfiles;
	read_inputs(inputfiles);
	int n_inputs = (int)inputfiles.size();
	for (int i = 0; i < n_inputs; ++i)
	{
		auto t1 = high_resolution_clock::now();

		str speciesfile, reactionsfile, discretefile;
		int maxitr_LM, maxitr_NR;
		double lmd0, nu, chem_gamma, elec_gamma, difu_gamma;
		read_input(inputfiles[i], speciesfile, reactionsfile, discretefile,
			maxitr_LM, maxitr_NR, lmd0, nu, chem_gamma, elec_gamma, difu_gamma);

		Chemical Chem(speciesfile, reactionsfile);
		FDM myFDM(discretefile, Chem);

		std::string datadir = "../data/simulation/" + inputfiles[i];
		std::filesystem::create_directories(datadir);

		std::cout << inputfiles[i] << std::endl;
		Chem.print_chem(datadir);
		myFDM.print_points(datadir);
		myFDM.print_etch2D(
			datadir, maxitr_LM, maxitr_NR,
			lmd0, nu, chem_gamma, elec_gamma, difu_gamma);

		std::cout << "\n=== equation solved ===" << std::endl;

		auto t2 = high_resolution_clock::now();
		duration<double, std::milli> ms_double = t2 - t1;
		std::cout << ms_double.count() << "ms\n";
	}
	return 0;
}
