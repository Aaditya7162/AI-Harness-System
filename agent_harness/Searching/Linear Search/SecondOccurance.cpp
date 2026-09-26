#include <bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i=0;i<n;i++){
        cin>>a[i];
    }
    int x;
    cin>>x;
    int first=-1, second=-1;
    for (int i=0;i<n;i++){
        if (a[i]==x){
            if(first==-1) first=i;
            else second=i;
        }
    }
    cout<<"first: "<<first<<" Second: "<<second<<endl;
}