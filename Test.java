import java.util.List;
import java.util.ArrayList;

public class Test {
	public
		static
	void main(String args[]) {
		System.out.println("Hello");
	 List<Point> pointList = new ArrayList<Point>();
Point p = new Point(5, 3);
	 	pointList.add(p);
		String formattedString = "  a  a\ta	a	a";
		System.out.println("Here is a formatted string: "+formattedString);
System.out.println(pointList);
   System.exit(0);
	}
}

