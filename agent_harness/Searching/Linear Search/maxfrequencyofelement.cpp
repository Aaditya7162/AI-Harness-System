#include <bits/stdc++.h>
using namespace std;

int main(){
    int a;
    cin >> a;
    vector<int> b(a);
    for(int i = 0; i < a; i++){
        cin >> b[i];
    }
    int max=INT_MIN;
    for (int i=0;i<a;i++){
        if (max<b[i]){
            max=b[i];
        }
    }
    vector<int> freq(max+1, 0);
    for (int i=0;i<a;i++){
        freq[b[i]]++;
    }
    for (int i=0;i<=max;i++){
        cout<<i<<" occurs "<<freq[i]<<endl;
    }
}