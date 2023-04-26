
import java.sql.*; // JDBC stuff.
import java.util.Properties;

public class PortalConnection {

    // Set this to e.g. "portal" if you have created a database named portal
    // Leave it blank to use the default database of your database user
    static final String DBNAME = "";
    // For connecting to the portal database on your local machine
    static final String DATABASE = "jdbc:postgresql://localhost/"+DBNAME;
    static final String USERNAME = "postgres";
    static final String PASSWORD = "postgres";

    // For connecting to the chalmers database server (from inside chalmers)
    // static final String DATABASE = "jdbc:postgresql://brage.ita.chalmers.se/";
    // static final String USERNAME = "tda357_nnn";
    // static final String PASSWORD = "yourPasswordGoesHere";


    // This is the JDBC connection object you will be using in your methods.
    private Connection conn;

    public PortalConnection() throws SQLException, ClassNotFoundException {
        this(DATABASE, USERNAME, PASSWORD);  
    }

    // Initializes the connection, no need to change anything here
    public PortalConnection(String db, String user, String pwd) throws SQLException, ClassNotFoundException {
        Class.forName("org.postgresql.Driver");
        Properties props = new Properties();
        props.setProperty("user", user);
        props.setProperty("password", pwd);
        conn = DriverManager.getConnection(db, props);
    }


    private static final String SQL_INSERT = "INSERT INTO Registrations VALUES (?,?)";

    // Register a student on a course, returns a tiny JSON document (as a String)
    public String register(String student, String courseCode){
      try (PreparedStatement reg = conn.prepareStatement(SQL_INSERT)) {
        reg.setString(1, student);     // student in the dirst parameter when inserting 
        reg.setString(2, courseCode);  // course is the second
        //reg.setString(3, "registered");
        reg.executeUpdate();  // does not work without this
        return "{\"success\":true}";
      
      // Here's a bit of useful code, use it or delete it 
       } catch (SQLException e) {
          return "{\"success\":false, \"error\":\""+getError(e)+"\"}";
       }     
    }

    //private static final String SQL_DELETE = "DELETE FROM Registrations WHERE student=? AND course=?";

    // Unregister a student from a course, returns a tiny JSON document (as a String)
    public String unregister(String student, String courseCode){
      String sid = student;
      String code = courseCode;
      String query = "DELETE FROM Registrations WHERE student='"+sid+"' AND course='"+code+"'"; // SQL injection
      try (Statement s = conn.createStatement();){
        int r = s.executeUpdate(query);
        if (r == 0)
          return  "{\"success\":false, \"error\": \"The student is not registered/in the waiting list or the course does not exist\"}";
        else
          return "{\"success\":true}";

      } catch (SQLException e){
        
        return "{\"success\":false, \"error\":\""+getError(e)+"\"}";
      }
     /*  try (PreparedStatement del = conn.prepareStatement(SQL_DELETE)) {
        del.setString(1, student);      
        del.setString(2, courseCode);  
        
        int rows = del.executeUpdate();
        if (rows != 0) {
          return "{\"success\":true}";
        }

        else return "{\"success\":false, \"error\": \"The student is not registered/in the waiting list or the course does not exist\"}";
      } 
      catch (SQLException e) {
        return "{\"success\":false, \"error\":\""+getError(e)+"\"}";
      }*/
    }

    /*the basic information, taken and registered/waiting courses, and everything from PathToGraduation */
    // Return a JSON document containing lots of information about a student, it should validate against the schema found in information_schema.json
    public String getInfo(String student) throws SQLException{
        
       /*  try(PreparedStatement st = conn.prepareStatement(
            // replace this with something more useful
            "SELECT jsonb_build_object('student',idnr,'name',name) AS jsondata FROM BasicInformation WHERE idnr=?"
            );){

              String taken = "json_agg(json_build_object )";
            
            st.setString(1, student);
            
            ResultSet rs = st.executeQuery();
            
            if(rs.next())
              return rs.getString("jsondata");
            else
              return "{\"student\":\"does not exist :(\"}"; 
            
        } */

        try(PreparedStatement st = conn.prepareStatement(
                        """
                        SELECT jsonb_build_object(
                        'student',idnr,
                        'name', name,
                        'login', login,
                        'program', program,
                        'branch', branch,
                        'finished', (
                            SELECT json_agg(jsonb_build_object(
                                'course', Courses.name,
                                'code',FinishedCourses.course,
                                'credits',FinishedCourses.credits,
                                'grade',FinishedCourses.grade))
                            FROM
                                FinishedCourses
                            JOIN
                                Courses
                            ON
                                Courses.code = FinishedCourses.course
                            WHERE
                                FinishedCourses.student = idnr),
                        'registered', (
                            SELECT json_agg(jsonb_build_object(
                                'course', Courses.name,
                                'code', Registrations.course,
                                'status', Registrations.status,
                                'position',Waitinglist.position
                                ))
                            FROM
                                Registrations
                            JOIN
                                Courses
                            ON
                                Courses.code = Registrations.course
                            LEFT JOIN
                                WaitingList
                            ON
                                Waitinglist.student = Registrations.student
                                AND
                                Waitinglist.course = Registrations.course
                            WHERE
                                Registrations.student = idnr),
                        'seminarCourses',seminarCourses,
                        'mathCredits',mathCredits,
                        'researchCredits',researchCredits,
                        'totalCredits',totalCredits,
                        'canGraduate',qualified) AS jsondata
                        FROM
                            BasicInformation
                        JOIN
                            PathToGraduation
                        ON
                            BasicInformation.idnr = PathToGraduation.student
                        WHERE
                            idnr=?
                        GROUP BY(Basicinformation.idnr, Basicinformation.name, BasicInformation.login, basicinformation.program, basicinformation.branch, pathtograduation.seminarcourses, pathtograduation.mathcredits, pathtograduation.researchcredits, pathtograduation.totalcredits, pathtograduation.qualified)"""))
        {
            st.setString(1, student);
            
            ResultSet rs = st.executeQuery();
            
            if(rs.next())
              return rs.getString("jsondata");
            else
              return "{\"student\":\"does not exist :(\"}"; 
            
        } 
    }

    // This is a hack to turn an SQLException into a JSON string error message. No need to change.
    public static String getError(SQLException e){
       String message = e.getMessage();
       int ix = message.indexOf('\n');
       if (ix > 0) message = message.substring(0, ix);
       message = message.replace("\"","\\\"");
       return message;
    }
}