xq1 = np.array([0,-25,0,25])
yq1 = np.array([0,35,70,35])

xq2 = np.array([0,0,80,80])
yq2 = np.array([0,35,35,0])

B = array([
# hold off
# axis([0 640 0 480 ])
# [X,Y] = ginput(4)
# plot([X;X(1)],[Y;Y(1)],'r')
# hold
# plot([0 0 640 640 0], [0 480 480 0 0],'b')
# axis([ -100 900 -100 580 ])
# Xp=[0;   0; 640; 640];
# Yp=[0; 480; 480;   0];
# B = [ X Y ones(size(X)) zeros(4,3)        -X.*Xp -Y.*Xp ...
#       zeros(4,3)        X Y ones(size(X)) -X.*Yp -Y.*Yp ];
# B = reshape (B', 8 , 8 )';
# D = [ Xp , Yp ];
# D = reshape (D', 8 , 1 );
# l = inv(B' * B) * B' * D;
# A = reshape([l(1:6)' 0 0 1 ],3,3)';
# C = [l(7:8)' 1];
# while 1 ,
# [x1,y1]=ginput(1); 
# [x2,y2]=ginput(1);
# for u=0:.1:1,
#   x = u*x1+(1-u)*x2;
#   y = u*y1+(1-u)*y2;
#   plot(x,y,'xr'); t=A*[x;y;1]/(C*[x;y;1]);plot(t(1),t(2),'ob') 
#   end
# end