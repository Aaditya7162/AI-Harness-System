#include <bits/stdc++.h>
using namespace std;
int main(){
    int n,ans=-1;
    cin>>n;
    int a[n];
    for (int k=0;k<n;k++){
        cin>>a[k];
    }
    int x;
    cin>>x;
    
    int i=0;
    int j=n-1;
    while(i<=j){
        int mid=i+(j-i)/2;
        if (a[mid]==x){
            ans=mid;
            break;
        }
        else if (a[mid]<x){
            i=mid+1;
        }
        else{
            j=mid-1;
        }
    }
    if(ans==-1){
        cout<<"Element Not Found";
    }
    else{
        cout<<"Element Found at index: "<<ans;
    }
}