/**
 * A:
 * 1 3
 * 5 7
 * 
 * B:
 * 2 4
 * 6 8
 * 
 * C:
 * 20 28
 * 52 76
 */ 


void matmul(int m, int n, int k, int* A, int* B, int* C){
    for(int i = 0; i < k; i++){
        for(int j = 0; j < m; j++){
            int partial_sum = 0;
            for(int l = 0; l < n; l++){
                partial_sum = partial_sum + A[j * m + l] * B[l * n + i];
            }
            C[j * m + i] = partial_sum;
        }
    }
}