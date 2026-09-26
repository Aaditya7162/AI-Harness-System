#include <bits/stdc++.h>
using namespace std;
int main(){
    int a,f=-1,e=-1;
    cin>>a;
    vector<int> b(a);
    for (int i=0;i<a;i++){
        cin>>b[i];
    }
    int c;
    cin>>c;
    for (int i=0;i<a;i++){
        if (b[i]==c){
            if(f==-1) f=i;
            else e=i;
        }
    }
    cout<<"first: "<<f<<" Second: "<<e<<endl;
}