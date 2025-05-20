#include <iostream>
#include <fstream>
#include <sstream>
#include "readCSV.hpp"

using str = std::string;

str readstr(std::ifstream& myfile)
{
	str line, element;
	std::getline(myfile, line);
	std::stringstream ss(line);
	std::getline(ss, element, ',');
	std::getline(ss, element, ',');
	return element;
}

void read_inputs(std::vector<str>& inputs)
{
	str filename = "../input/inputs.csv";
	std::ifstream myfile(filename);
	if(!myfile.is_open())
	{
		std::cerr << "error while opening file" << filename << "\n";
		return;
	}

	str line, element;
	std::getline(myfile, line);
	std::stringstream mystring(line);

	inputs.reserve(30);
	while (std::getline(mystring, element, ','))
	{
		inputs.emplace_back(element);
	}
	myfile.close();
}

void read_input(str& inputfile,
	str& speciesfile, str& reactionsfile, str& discretefile,
	int& maxitr_LM, int& maxitr_NR, double& lmd, double& nu,
	double& chem_gamma, double& elec_gamma, double& difu_gamma)
{
	str inputdir = "../input/";
	str filename = inputdir + "input/" + inputfile + ".csv";
	std::ifstream myfile(filename);
	if (!myfile.is_open())
	{
		std::cerr << "error while opening file " << filename << '\n';
		return;
	}

	speciesfile = inputdir + "species/" + readstr(myfile);
	reactionsfile = inputdir + "reactions/" + readstr(myfile);
	discretefile = inputdir + "discrete/" + readstr(myfile);
	maxitr_LM = std::stoi(readstr(myfile));
	maxitr_NR = std::stoi(readstr(myfile));
	lmd = std::stod(readstr(myfile));
	nu = std::stod(readstr(myfile));
	chem_gamma = 1.0 - std::stod(readstr(myfile));
	elec_gamma = 1.0 - std::stod(readstr(myfile));
	difu_gamma = 1.0 - std::stod(readstr(myfile));

	myfile.close();
}
