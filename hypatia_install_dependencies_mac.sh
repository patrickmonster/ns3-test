# satgenpy
echo "Installing dependencies for satgenpy..."
python -m pip install numpy astropy ephem networkx sgp4 geopy matplotlib statsmodels || exit 1
brew install projectm libgee libprotoident || exit 1
brew install --cask profind

brew install python3-pip || exit 1
# Mac alternatives (to be able to pip install cartopy)
# brew install proj geos
# export CFLAGS=-stdlib=libc++
# MACOSX_DEPLOYMENT_TARGET=10.14
pip install git+https://github.com/snkas/exputilpy.git@v1.6 || exit 1
pip install cartopy || exit 1

# ns3-sat-sim
echo "Installing dependencies for ns3-sat-sim..."
brew install open-mpi open-completion libopenmpt lcov gnuplot || exit 1
brew install --cask open-in-code || exit
pip install numpy statsmodels || exit 1
pip install git+https://github.com/snkas/exputilpy.git || exit 1
git submodule update --init --recursive || exit 1

wget https://www.nsnam.org/releases/ns-allinone-3.37.tar.bz2
tar -xvf ns-allinone-3.37.tar.bz2


# satviz
echo "There are currently no dependencies for satviz."

# paper
echo "Installing dependencies for paper..."
pip install numpy || exit 1
pip install git+https://github.com/snkas/exputilpy.git@v1.6 || exit 1
pip install git+https://github.com/snkas/networkload.git@v1.3 || exit 1
brew install-y gnuplot

# Confirmation dependencies are installed
echo ""
echo "Hypatia dependencies have been installed."

