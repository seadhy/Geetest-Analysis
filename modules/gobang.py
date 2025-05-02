import numpy as np


class GobangSolver:
    def __init__(self, ques: list):
        self.ques = ques
        
    def __check_line(self, arr, unique_arr):
        return np.count_nonzero(arr == 0) == 1 and len(unique_arr) == 2
    
    def found_last_piece(self):
        arr = np.array(self.ques)
        diagonal = np.diagonal(arr)
        unique_diagonal = np.unique(diagonal)
        
        if self.__check_line(diagonal, unique_diagonal):
            x = int(np.where(diagonal == 0)[0][0])
            target_coordinate = (x, x)
            
            target_color = unique_diagonal[unique_diagonal != 0][0]
    
            np.fill_diagonal(arr, 0)
            piece_coordinate_y, piece_coordinate_x = np.where(arr == target_color)
            
            piece_coordinate_x = int(piece_coordinate_x[0])
            piece_coordinate_y = int(piece_coordinate_y[0])
            
            return {'target': target_coordinate, 'piece': (piece_coordinate_x, piece_coordinate_y)}
        
        reversed_arr = np.fliplr(arr)
        reversed_diagonal = np.diagonal(reversed_arr)    
        reversed_unique_diagonal = np.unique(reversed_diagonal)
            
        if self.__check_line(reversed_diagonal, reversed_unique_diagonal):
            x = int(np.where(reversed_diagonal == 0)[0][0])
            target_coordinate = [x, x]
            
            target_color = reversed_unique_diagonal[reversed_unique_diagonal != 0][0]
    
            np.fill_diagonal(reversed_arr, 0)
            piece_coordinate_y, piece_coordinate_x = np.where(reversed_arr == target_color)
            
            piece_coordinate_x = int(piece_coordinate_x[0])
            piece_coordinate_y = int(piece_coordinate_y[0])
            
            return {'piece': [piece_coordinate_x, piece_coordinate_y], 'target': target_coordinate}
    
        for y, row in enumerate(arr):
            unique_row = np.unique(row)
            if self.__check_line(row, unique_row):           
                x = int(np.where(row == 0)[0][0])
                target_coordinate = [y, x]                
                
                target_color = unique_row[unique_row != 0][0]
                
                arr[y, :] = 0
                
                piece_coordinate_y, piece_coordinate_x = np.where(arr == target_color)
                    
                piece_coordinate_x = int(piece_coordinate_x[0])
                piece_coordinate_y = int(piece_coordinate_y[0])
                
                return {'piece': [piece_coordinate_y, piece_coordinate_x], 'target': target_coordinate}
    
        
        for x, column in enumerate(arr.T):
            unique_column = np.unique(column)
    
            if self.__check_line(column, unique_column):
                y = int(np.where(column == 0)[0][0])
                target_coordinate = [y, x]
                
                target_color = unique_column[unique_column != 0][0]
                            
                arr.T[x, :] = 0
                piece_coordinate_x, piece_coordinate_y = np.where(arr.T == target_color)
                    
                piece_coordinate_x = int(piece_coordinate_x[0])
                piece_coordinate_y = int(piece_coordinate_y[0])
                
                return {'piece': [piece_coordinate_y, piece_coordinate_x], 'target': target_coordinate}
      
      
if __name__ == '__main__':
    # debugging
    
    # diagonal_ques =  [[4, 4, 2, 2, 1], [2, 4, 1, 1, 3], [0, 0, 4, 3, 3], [2, 1, 2, 0, 2], [1, 0, 0, 1, 4]]
    # horizantal_ques = [[0, 1, 0, 0, 0], [0, 2, 1, 0, 4], [3, 0, 1, 0, 0], [1, 3, 0, 0, 0], [2, 2, 0, 2, 2]]
    # vertical_ques = [[1, 4, 1, 0, 3], [2, 0, 1, 2, 4], [3, 3, 1, 2, 0], [3, 0, 1, 2, 1], [1, 4, 3, 2, 3]]
    
    test = [[1, 0, 2, 4, 2], [3, 0, 3, 0, 2], [0, 0, 1, 0, 2], [0, 0, 0, 0, 2], [0, 0, 0, 0, 0]]
    print(np.array(test))
    # print(found_last_piece(diagonal_ques))
    # print(found_last_piece(horizantal_ques))
    # print(found_last_piece(vertical_ques))
    print(GobangSolver(ques=test).found_last_piece(test))
    