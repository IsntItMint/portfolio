#include "FDM_maker.hpp"

void FDM_maker::get_L()
{
	SpMat AG(n3d, n3d);
	get_OmegaL(AL);
	get_GammaL(AG);
	AL += AG;
	AL.prune(0.0);
	AL.makeCompressed();
}

void FDM_maker::get_R()
{
	SpMat AG(n3d, n3d);
	get_OmegaR(AR);
	get_GammaR(AG);
	AR += AG;
	AR.prune(0.0);
	AR.makeCompressed();
}

void FDM_maker::get_D()
{
	SpMat AG(n3d, n3d);
	get_OmegaD(AD);
	get_GammaD(AG);
	AD += AG;
	AD.prune(0.0);
	AD.makeCompressed();
}

void FDM_maker::get_U()
{
	SpMat AG(n3d, n3d);
	get_OmegaU(AU);
	get_GammaU(AG);
	AU += AG;
	AU.prune(0.0);
	AU.makeCompressed();
}
