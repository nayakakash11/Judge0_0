#include <iostream>
#include <vector>
#include <string>
using namespace std;

string longestCommonPrefix(vector<string>& strs) {
    if (strs.empty()) return "-1";
    
    string prefix = strs[0];
    
    for (int i = 1; i < strs.size(); ++i) {
        while (strs[i].find(prefix) != 0) {  // Not a prefix
            prefix = prefix.substr(0, prefix.size() - 1);
            if (prefix.empty()) return "-1";
        }
    }
    return prefix;
}

int main() {
    int n;
    while (cin >> n) { // Read until EOF
        vector<string> words(n);
        for (int i = 0; i < n; ++i) {
            cin >> words[i];
        }
        cout << longestCommonPrefix(words) << endl;
    }
    return 0;
}