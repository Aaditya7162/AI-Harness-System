#include <bits/stdc++.h>
using namespace std;
int main(){
    int n;
    cin >> n;
    vector<int> a(n);
    for(int i = 0; i < n; i++){
        cin >> a[i];
    }
    int max=INT_MIN;
    for (int i=0;i<n;i++){
        if (max<a[i]){
            max=a[i];
        }
    }
    vector<int> freq(max+1, 0);
    for (int i=0;i<n;i++){
        freq[a[i]]++;
        if (freq[a[i]]==2){
            cout<<a[i]<<endl;
            break;
        }
    }
}