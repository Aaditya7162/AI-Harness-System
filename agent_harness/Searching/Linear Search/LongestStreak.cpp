#include <bits/stdc++.h>
using namespace std;
int main(){
    int a,count=1,ans=1;
    cin>>a;
    int b[a];
    for (int i=0;i<a;i++){
        cin>>b[i];
    }
    for (int i=0;i<a-1;i++){
        if (b[i]+1==b[i+1]){
            count++;
        }
        else{
            count=1;
        }
        ans=max(ans,count);
    }
    cout<<ans;
}