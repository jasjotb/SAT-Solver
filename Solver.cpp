#include<bits/stdc++.h>

using namespace std;
//Unit Propagation Part
int unitprop(vector<vector<int>>&f) {
    int len,i;
    len=f.size();
    for(i=0;i<len;i++) {
        if(f[i].size()==1) return f[i][0];
    }    
    return 0;
}

//Pure Literals
int pure(vector<vector<int>>&f,int n) {
    int y[2*n],i,j,len;
    for(i=0;i<2*n;i++) y[i]=0;
    len=f.size();
    for(i=0;i<len;i++) {
        for(j=0;j<f[i].size();j++) {
            if(f[i][j]>0) {
                y[2*f[i][j]-2]=1;
            }
            else y[(-2)*f[i][j]-1]=1;

        }
    }
    for(i=0;i<2*n;i+=2) {
        if(y[i]!=y[i+1]) {
            if(y[i]==1) return i;
            else return i+1;
        }
        
    }
    return -2;
}


vector<vector<int>> update1(vector<vector<int>>&f,vector<int>x, int a){    
    int len,i,z,j;
    len=f.size();
    vector<vector<int>>f3;
    for(i=0;i<len;i++) {
        vector<int>v;
        z=0;
        for(j=0;j<f[i].size();j++) {
            if(f[i][j]==a) {
                z=1;
                break;
            }
            else if(f[i][j]!=-1*a) v.push_back(f[i][j]);

        }
        if(z!=1) f3.push_back(v);
    }
    return f3;
}

int check(vector<vector<int>>&f) {
    int len,i;
    len=f.size();
    for(i=0;i<len;i++) {
        if(f[i].size()==0) return 1;
    }
    return 0;
}

void dpll(vector<vector<int>>f, vector<int>x,int n, int l,int&sol,int*ans,vector<pair<int,int>>count) {
    int i,a,b;
    if(f.size()==0) {
        sol=1;
        for(i=0;i<n+1;i++) ans[i]=x[i];
        return;
    }
    vector<vector<int>>f1;    
        f1=f;
    if(sol==0){
    a=unitprop(f1);
    
     while(a!=0) {
        if(a<0) x[-a]=0;
        else x[a]=1;
        
        f1=update1(f1,x,a);
        if(check(f1)) {         
            f1.clear();
            f1.shrink_to_fit();
            return;
        }
        if(f1.size()==0) {
            sol=1;
            for(i=0;i<n+1;i++) ans[i]=x[i];
            return;
        }
        a=unitprop(f1);
    }

    int b=pure(f1,n);

    if(b%2) {
        b=-(b/2+1);
    }
    else b=b/2+1;
    if(b!=0) {
        if(b<0) x[-b]=0;
        else x[b]=1;
        
        f1=update1(f1,x,b);
        if(check(f1)) {
            f1.clear();
            f1.shrink_to_fit();
            return;
        }
        if(f1.size()==0) {
        sol=1;
        for(i=0;i<n+1;i++) ans[i]=x[i];
        return;
    }
    }
        for(i=1;i<=n;i++) {
             if(x[count[i].second]==-1) {
                x[count[i].second]=1;
                vector<vector<int>>f5;
                f5=update1(f1,x,count[i].second);
                dpll(f5,x,n,count[i].second,sol,ans,count);
                
                if(sol==1) return;
                
                x[count[i].second]=0;
                f5=update1(f1,x,-count[i].second);
                dpll(f5,x,n,count[i].second,sol,ans,count);
                
                if(sol==1) return;
                
                
            }
        }
    }
}
int main() {
    freopen("input.cnf","r",stdin);
    char c;
        string s;
    while(true){
        cin >> c;
        if(c == 'c'){
            getline(cin,s);
        }
        else{
            cin >> s;
            break;
        }
    }
    int n,p,i,a;
    cin >> n >> p;
    vector<int>x(n+1,-1);
    vector<pair<int,int>>count;
    for(i=0;i<n+1;i++) {
        pair<int,int>r1(0,i);
        count.push_back(r1);
    }
    vector<vector<int>> f;
    for(i=0;i<p;i++) {
        vector<int>v;
        cin>>a;
        while(a!=0) {
            v.push_back(a);
            if(a>0) count[a].first+=1;
            else count[-a].first+=1;
            cin>>a;
        }

        f.push_back(v);
    }  
    sort(count.rbegin(),count.rend()-1);
    int sol=0;
    int ans[n+1];
    for(i=0;i<n+1;i++) ans[i]=-1;
    dpll(f,x,n,0,sol,ans,count);
    int final_answer[n+1];
    for(i=1;i<=n;i++){
        if(ans[i] == 1 || ans[i] == -1){
            final_answer[i] = i;
        }
        else{
            final_answer[i] = -i;
        }
    }
    
    if(sol==0) cout<<"UNSAT";
    else {
        cout<<"SAT"<<'\n';
        for(i=1;i<=n;i++) {
            cout << final_answer[i] << ' ';
        }
    }
}