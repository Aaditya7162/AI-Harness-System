#include <bits/stdc++.h>
using namespace std;

int main() {
    int n, x;
    cin >> n >> x;

    vector<int> a(n);
    for (int i = 0; i < n; i++) cin >> a[i];

    int closest = a[0];

    for (int i = 1; i < n; i++) {
        if (abs(a[i] - x) < abs(closest - x)) {
            closest = a[i];
        }
    }

    cout << closest;
}