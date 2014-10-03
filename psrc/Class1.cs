using System;
using System.Collections.Generic;
using System.IO;
using ps = Photoshop;

namespace psrc
{
    public class PSObject
    {
        private ps.Application app = new ps.Application();

        public List<string> getOpenedDocument()
        {
            List<string> arr = new List<string>();
            ps.Documents docs = app.Documents;
            foreach (ps.Document doc in docs)
            {
                arr.Add(doc.Name);
            }
            return arr;
        }

        public void executeJSScript(string path)
        {
            try
            {
                if (!File.Exists(path))
                    throw new Exception("File not found");
                app.DoJavaScriptFile(path, (object)null, (object)null);
            }
            catch (Exception ex)
            {
                throw ex;
            }
        }
    }
}
