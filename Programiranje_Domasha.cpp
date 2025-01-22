#include <iostream>
#include <vector>
#include <ctime>
#include <climits>
#include <cstdlib>

using namespace std;

class SegmentTree{
private:
    vector<int> drvo;
    int n;

    void update(int node, int start, int end, int i, int val){
        if (start == end){
            drvo[node] = val;
            return;
        }
        int mid = (start+end)/2;
        if (start <= i && i <= mid){
            update(2*node, start, mid, i, val);
        }
        else{
            update(2*node+1, mid+1, end, i, val);
        }
        drvo[node] = drvo[2*node] + drvo[2*node+1];
    }

    void build(int node, int start, int end, const vector<int>& arr){
        if (start == end){
            drvo[node] = arr[start];
        }
        else{
            int mid = (start + end) / 2;
            build(2 * node, start, mid, arr);
            build(2 * node + 1, mid + 1, end, arr);
            drvo[node] = drvo[2 * node] + drvo[2 * node + 1];
        }
    }

    int minimun(int node, int start, int end, int L, int R){
        if (R < start || end < L){
            return INT_MAX;
        }
        if (L <= start && end <= R){
            return drvo[node];
        }
        int mid = (start + end) / 2;
        int levo = minimun(2 * node, start, mid, L, R);
        int desno = minimun(2 * node + 1, mid + 1, end, L, R);
        return min(levo, desno);
    }

    int maximun(int node, int start, int end, int L, int R){
        if (R < start || end < L){
            return INT_MIN;
        }
        if (L <= start && end <= R){
            return drvo[node];
        }
        int mid = (start + end) / 2;
        int levo = maximun(2 * node, start, mid, L, R);
        int desno = maximun(2 * node + 1, mid + 1, end, L, R);
        return max(levo, desno);
    }

    int sum(int node, int start, int end, int L, int R){
        if (R < start || end < L){
            return 0;
        }
        if (L <= start && end <= R){
            return drvo[node];
        }
        int mid = (start + end) / 2;
        int levo = sum(2 * node, start, mid, L, R);
        int desno = sum(2 * node + 1, mid + 1, end, L, R);
        return levo + desno;
    }

public:
    SegmentTree(const vector<int>& arr){
        n = arr.size();
        drvo.resize(4 * n);
        build(1, 0, n - 1, arr);
    }
    void updateTree(int i, int val){
        update(1,0,n-1,i,val);
    }
    int sumQuery(int L, int R){
        return sum(1, 0, n - 1, L, R);
    }
    int minQuery(int L, int R){
        return minimun(1, 0, n - 1, L, R);
    }

    int maxQuery(int L, int R){
        return maximun(1, 0, n - 1, L, R);
    }
};

int main(){
    srand(time(0));
    int n = 30 + rand() % 171;
    vector<int> vec(n);

    for (int i = 0; i < n; i++){
        vec[i] = rand()%100;
    }

    return 0;
}
