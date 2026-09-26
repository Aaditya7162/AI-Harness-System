#include <bits/stdc++.h>
using namespace std;
int main(){
    int a;
    cin>>a;
    int b[a];
    for (int i=0;i<a;i++){
        cin>>b[i];
        if (b[i]!=i+1){
            cout<<i+1;
            break;
        }
    }
}