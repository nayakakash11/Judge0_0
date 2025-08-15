#include <bits/stdc++.h>
using namespace std;

pair<int, int> twoSumValues(const vector<int>& nums, int target) {
    unordered_set<int> seen
    for (int num : nums) {
        int complement = target - num;
        if (seen.count(complement)) {
            int a = min(num, complement);
            int b = max(num, complement);
            return {a, b};
        }
        seen.insert(num);
    }
    return {-1, -1};
}

int main() {
    int n, target;
    
    // Continue until input ends
    while (cin >> n) {
        cin >> target;
        vector<int> nums(n);
        for (int i = 0; i < n; ++i)
            cin >> nums[i];


        pair<int, int> result = twoSumValues(nums, target);
        if (result.first == -1)
            cout << -1 << "\n";
        else
            cout << result.first << " " << result.second << "\n";
    }

    return 0;
}