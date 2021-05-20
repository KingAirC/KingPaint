#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void rref(int row, int col, double mat[][col]) {
	int i = 0, j = 0, t, p;
	double matTJ, matIJ, temp;

	while (i < row && j < col) {
		if (mat[i][j] != 0) {
			for (t = i + 1; t < row; t++) {
				if (mat[i][j] != 0) {
					matTJ = mat[t][j];
					for (p = j; p < col; p++) {
						mat[t][p] -= matTJ * mat[i][p] / mat[i][j];
					}
				}
			}
			matIJ = mat[i][j];
			for (p = j; p < col; p++) {
				mat[i][p] /= matIJ;
			}
			for (t = 0; t < i; t++) {
				matTJ = mat[t][j];
				for (p = j; p < col; p++) {
					mat[t][p] -= mat[i][p] * matTJ;
				}
			}
			i++;
			j++;
		} else {
			for (t = i + 1; t < row; t++) {
				if (mat[t][j] != 0) {
					break;
				}
			}
			if (t == row) {
				j++;
			} else {
				for (p = j; p < col; p++) {
					temp = mat[t][p];
					mat[t][p] = mat[i][p];
					mat[i][p] = temp;
				}
			}
		}
	}
}
