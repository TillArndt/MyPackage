
function dbs_query {
  dbs search --url="https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet" --query "find file where dataset = $2" | grep htholen > $1
}

