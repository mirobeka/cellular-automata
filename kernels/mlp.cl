__kernel void next_state(__global cell* cells, __global cell* new_cells){
  int gid = get_global_id(0);
  new_cells[gid] = cells[gid];
  if(cells[gid].grayscale < 255){
    new_cells[gid].grayscale = cells[gid].grayscale+1;
  }else{
    new_cells[gid].grayscale = 0;
  }
}
