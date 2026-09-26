#include <bits/stdc++.h>
using namespace std;
int main(){
    int a;
    cin>>a;
    vector<int> b(a);
    vector<int> freq(10, 0);
    while(a>0){
        int r=a%10;
        freq[r]++;
        a/=10;
    }
    for (int i=0;i<10;i++){
        if (freq[i]!=0){
            cout<<i<<" occurs "<<freq[i]<<" times."<<endl;
        }
    }
}