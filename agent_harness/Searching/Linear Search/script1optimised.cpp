#include <bits/stdc++.h>
using namespace std;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int a; // number of elements
    if(!(cin>>a)) return 0;
    if(a<=0){
        cout << "First: -1 Second: -1\n";
        return 0;
    }
    vector<int> b(a);
    for(int i=0;i<a;i++) cin>>b[i];
    int c; cin>>c;
    int f=-1, e=-1;
    for(int i=0;i<a;i++){
        if(b[i]==c){
            if(f==-1) f=i;
            else e=i;
        }
    }
    cout << "First: " << f << " Second: " << e << "\n";
    return 0;
}
