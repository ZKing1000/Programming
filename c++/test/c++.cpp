#include "iostream"
#include <vector>
using namespace std;
int main(){
	vector<int> vec;
	for(int i;i<10;i++){
		vec.push_back(i);
	}
	cout << vec[1] << endl;
	cout << vec.size() << endl;
	//vec.erase(vec.begin()+3);
}
