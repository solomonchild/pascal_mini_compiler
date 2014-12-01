procedure TCalcDisplay.Draw; 
var   
    Color: Byte;   
  I: Integer; 
  B: TDrawBuffer; 
begin 
    Key := UpCase(Key); 
    if(Status=csError) and (Key<>'C') then  
       Key:=' '; 
    Color := GetColor(1); 
    I := Size.X - Length(Number) - 2; 
    MoveChar(B, ' ', Color, Size.X); 
    MoveChar(B[I], Sign, Color, 1); 
    MoveStr(B[I + 1], Number, Color); 
    WriteBuf(0, 0, Size.X, 1, B); 
end;
