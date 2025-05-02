import numpy as np


class IconCrusherSolver:
    def __init__(self, ques: list):
        self.ques = ques
        
    def find_icon_swap(self):
        arr = np.array(self.ques) 
        
        for x, column in enumerate(arr):
            unique_column, counts = np.unique(column, return_counts=True) 
            if len(unique_column) == 2:
                icon = unique_column[counts == 2][0]        
                               
                unique_icon = unique_column[counts == 1][0]            
                unique_icon_index = int(np.where(column == unique_icon)[0][0])
                            
                missing_icon_x = None
                if x == 0:
                    if icon == arr[x + 1][unique_icon_index]:
                        missing_icon_x = x + 1
                elif x == 1:
                    if icon == arr[x - 1][unique_icon_index]: 
                        missing_icon_x = x - 1
                    elif icon == arr[x + 1][unique_icon_index]:
                        missing_icon_x = x + 1
                elif x == 2:
                    if icon == arr[x - 1][unique_icon_index]:
                        missing_icon_x = x - 1
                
                if missing_icon_x is not None:
                    target_icon_coordinate = [x, unique_icon_index]
                    missing_icon_coordinate = [missing_icon_x, unique_icon_index]
                    return {'missing_icon': missing_icon_coordinate, 'target_icon': target_icon_coordinate}
                
        for y, row in enumerate(arr.T):
            unique_row, counts = np.unique(row, return_counts=True)
            if len(unique_row) == 2:
                icon = unique_row[counts == 2][0]        
                               
                unique_icon = unique_row[counts == 1][0]            
                unique_icon_index = int(np.where(row == unique_icon)[0][0])
                
                missing_icon_y = None
                if y == 0:
                    if icon == arr.T[y + 1][unique_icon_index]:
                        missing_icon_y = y + 1
                elif y == 1:
                    if icon == arr.T[y - 1][unique_icon_index]: 
                        missing_icon_y = y - 1
                    elif icon == arr.T[y + 1][unique_icon_index]:
                        missing_icon_y = y + 1
                elif y == 2:
                    if icon == arr.T[y - 1][unique_icon_index]:
                        missing_icon_y = y - 1
                
                if missing_icon_y is not None:
                    target_icon_coordinate = [unique_icon_index, y]
                    missing_icon_coordinate = [unique_icon_index, missing_icon_y]
                    return {'missing_icon': missing_icon_coordinate, 'target_icon': target_icon_coordinate}


if __name__ == '__main__':
    # debugging
    
    ques = [[2, 1, 2], [1, 0, 3], [1, 3, 2]]
    print(IconCrusherSolver(ques=ques).find_icon_swap())
