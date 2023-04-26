public class TestPortal {

   // enable this to make pretty printing a bit more compact
   private static final boolean COMPACT_OBJECTS = false;

   // This class creates a portal connection and runs a few operation

   // \i setup.sql \i triggers.sql
   // select * from registrations;
   // select * from waitinglist;

   /* \c postgres
\set QUIT true
SET client_min_messages TO NOTICE;
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
\set QUIET false */

   public static void main(String[] args) {
      try{
         PortalConnection c = new PortalConnection();
   
         // Write your tests here. Add/remove calls to pause() as desired. 
         // Use println instead of prettyPrint to get more compact output (if your raw JSON is already readable)

         // 1
         prettyPrint(c.getInfo("7777777777")); // List info
         pause();

         // 2
         System.out.println(c.register("7777777777", "CCC111")); // Register pass
         pause();

         // 3
         System.out.println(c.register("7777777777", "CCC111")); // Again error
         pause();

         // 4
         System.out.println(c.unregister("7777777777", "CCC111")); // Unregister pass
         pause();
         
         System.out.println(c.unregister("7777777777", "CCC111")); // again error
         pause();
        
         // 5
         System.out.print(c.register("7777777777", "CCC333")); // should give error, student has not read CCC444
         pause();

         // 6
         System.out.print(c.unregister("1111111111", "CCC666")); // unregister from full course with queue
         pause();

         System.out.print(c.register("1111111111", "CCC666")); // should be placed last in the queue
         pause();

         // 7
         System.out.print(c.unregister("1111111111", "CCC666")); // unregister again
         pause();

         System.out.print(c.register("1111111111", "CCC666")); // register again
         pause();

         // 8
         System.out.println(c.unregister("1111111111", "CCC777")); //unregister from full course
         pause();

         // 9
         System.out.println(c.unregister("1111111111", "x' OR 'a'='a")); // injection

   
         /*System.out.println(c.unregister("3333333333", "CCC333")); 
         pause();

         prettyPrint(c.getInfo("2222222222")); 
         pause();

         System.out.println(c.register("2222222222", "CCC111")); 
         pause();

         prettyPrint(c.getInfo("2222222222"));*/



      
      } catch (ClassNotFoundException e) {
         System.err.println("ERROR!\nYou do not have the Postgres JDBC driver (e.g. postgresql-42.5.1.jar) in your runtime classpath!");
      } catch (Exception e) {
         e.printStackTrace();
      }
   }
   
   
   
   public static void pause() throws Exception{
     System.out.println("PRESS ENTER");
     while(System.in.read() != '\n');
   }
   
   // This is a truly horrible and bug-riddled hack for printing JSON. 
   // It is used only to avoid relying on additional libraries.
   // If you are a student, please avert your eyes.
   public static void prettyPrint(String json){
      System.out.print("Raw JSON:");
      System.out.println(json);
      System.out.println("Pretty-printed (possibly broken):");
      
      int indent = 0;
      json = json.replaceAll("\\r?\\n", " ");
      json = json.replaceAll(" +", " "); // This might change JSON string values :(
      json = json.replaceAll(" *, *", ","); // So can this
      
      for(char c : json.toCharArray()){
        if (c == '}' || c == ']') {
          indent -= 2;
          breakline(indent); // This will break string values with } and ]
        }
        
        System.out.print(c);
        
        if (c == '[' || c == '{') {
          indent += 2;
          breakline(indent);
        } else if (c == ',' && !COMPACT_OBJECTS) 
           breakline(indent);
      }
      
      System.out.println();
   }
   
   public static void breakline(int indent){
     System.out.println();
     for(int i = 0; i < indent; i++)
       System.out.print(" ");
   }   
}
