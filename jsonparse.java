import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import java.nio.file.Files;
import java.nio.file.Paths;

class jsonparse
{
  public static void main(String args[])
  {
    String file = "/cycolinks_textonly.json";
    String json = readFileAsString(file);
    json = json.substring(json.indexOf('{'),json.lastIndexOf(';')+1);
    JSONObject baseJsonResponse = new JSONObject(json);
    JSONObject d = baseJsonResponse.getJSONObject("d");
    JSONObject b = d.getJSONObject("b");
    JSONObject d2 = b.getJSONObject("d");
    JSONObject coupons = d2.getJSONObject("coupons");
    Map<String, JSONObject> map = (Map<String,JSONObject>)coupons.getMap();
    ArrayList<String> list = new ArrayList<String>(map.keySet());
    for(int i=0; i<list.size(); i++)
    {
      JSONObject code = coupons.getJSONObject(list.get(i));
      if(code.getString("name")!="")
      System.out.println("Code for "+code.getString("name")+" is : "+code.getString("code"));
    }
  }
}
