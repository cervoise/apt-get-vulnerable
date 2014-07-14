echo "You should have run an apt-get update (with root privilege) before runing this script."
#add a question did you have run? do you want to?
dpkg -l > input1.txt
apt-get --simulate upgrade > input2.txt