#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    int x;
    cin >> x;

    int ans = 0, c = 0;

    for (int i = 0; i < n; i++) {
        if (a[i] == x) {
            c++;
            ans = max(ans, c);
        } 
        else {
            c = 0;
        }
    }

    cout << ans << endl;
}