#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
    }
    // The numbers are from 1 to n+1 with exactly one missing.
    vector<bool> present(n + 2, false);
    for (int x : a) {
        if (x >= 1 && x <= n + 1) present[x] = true;
    }
    for (int i = 1; i <= n + 1; ++i) {
        if (!present[i]) {
            cout << i << "\n";
            break;
        }
    }
    return 0;
}
