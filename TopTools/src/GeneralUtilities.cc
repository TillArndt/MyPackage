
#include "Top/Tools/interface/GeneralUtilities.h"
#include <sstream>

using namespace std;
using namespace edm;
using namespace reco;
std::string GeneralUtilities::Table(std::map<std::string, std::vector<double> >  entries, std::vector<std::string> head)
{
  std::string table;
  for(std::vector<std::string>::const_iterator it0=head.begin(); it0 != head.end();++it0){
    table+= *it0;
    table += " \t ";
  }
  table += " \n ";
  for( std::map<std::string,std::vector<double> >::iterator it=entries.begin();  it != entries.end(); ++it){
    table+=it->first;
    for(std::vector<double>::const_iterator it2=it->second.begin(); it2 != it->second.end();++it2){
      table += " \t ";
      stringstream stream;
      stream << *it2;      
      table += stream.str();
    }
    table+= " \n";
  }
  return table;
}

double GeneralUtilities::Round(double Zahl, int Stellen)
{
    Zahl *= pow(10, Stellen);
    if (Zahl >= 0)
      Zahl = floor(Zahl + 0.5);
    else
      Zahl = ceil(Zahl - 0.5);
    Zahl /= pow(10, Stellen);
    return Zahl;
}

std::string GeneralUtilities::LatexTable(std::string label, std::string caption, std::vector<std::string> lines, std::vector<std::string> columns, std::vector<std::vector<double> > entries, std::vector<std::vector<double> > errorsPlus, std::vector<std::vector<double> > errorsMinus , int nachkommma)
{
  std::string table = "\\begin{table}[htb] \n \\centering \n \\renewcommand{\\arraystretch}{1.3} \n \\setlength{\\tabcolsep}{10pt} \n \\caption{";
  table += caption;
  table += "} \n \\begin{tabular}{ l";
  for(uint i=1; i< columns.size();++i){
    table +=" c ";
  }
  table += "} \n \\hline \n ";
  for(uint i=0; i< columns.size();++i){
    table += "\\textbf{";
    table += columns[i];
    if(i==(columns.size()-1))table += "} \\\\ \n \\hline \n ";
    else table += "} & ";
  }
  for(uint i=0; i< lines.size();++i){
    table += lines[i];
    table += " & ";
    for(uint j=1; j< columns.size(); ++j){
      table += " $";
      stringstream stream;
      stream << Round(entries[i][j],nachkommma);      
      table += stream.str();
//       if(Round(errorsPlus[i][j],nachkommma)==Round(errorsMinus[i][j],nachkommma)){       
// 	table += " \\pm ";
// 	stream.str("");
// 	stream << Round(errorsPlus[i][j],nachkommma);
// 	table += stream.str();
//       }
//       else{
      table += "^{+";
      stream.str("");
      stream << Round(errorsPlus[i][j],nachkommma);
      table += stream.str();
      table += "}_{-";
      stream.str("");
      stream << Round(errorsMinus[i][j],nachkommma);
      table += stream.str();
      table += "}";
      //      }
      table += "$ (stat.)";
      if(j==(columns.size()-1))table += " \\\\  \n ";
      else table += " & "; 
    }    
  }
  table += " \\hline \n  \\end{tabular} \n  \\label{tab:";
  table += label;
  table += "} \n \\end{table} \n ";
  return table;
}

double GeneralUtilities::ptVsJetaxis( reco::Track muon ,  const pat::JetRef  jetchosen  )
{
    
    double cosTheta = jetchosen->p4().Vect().Dot( muon.momentum() );
    if( jetchosen->p() != 0 )cosTheta = cosTheta / (jetchosen->p()*  muon.p()  );// cos(theta)
    return  std::sqrt(1 - cosTheta *cosTheta) * muon.p() ;// p * sin(theta) = pt

}
double GeneralUtilities::ptVsJetaxis( reco::Track muon ,  const pat::Jet &  jetchosen  )
{
    double cosTheta = jetchosen.p4().Vect().Dot( muon.momentum() );
    if( jetchosen.p() != 0 )cosTheta = cosTheta / (jetchosen.p() * muon.p());// cos(theta)
    return std::sqrt(1 - cosTheta *cosTheta) * muon.p() ;// p * sin(theta) = pt
}
double GeneralUtilities::ptVsJetaxis( const reco::GenParticleRef muon ,  const reco::GenParticleRef  bQuark)
{
    
    double cosTheta = bQuark->p4().Vect().Dot( muon->momentum() ); 
    if( bQuark->p() != 0 )cosTheta = cosTheta /( bQuark->p() * muon->p() );// cos(theta)
    return std::sqrt(1 - cosTheta *cosTheta) * muon->p() ;// p * sin(theta) = pt
}
double GeneralUtilities::ptVsJetaxis(const reco::Candidate& muon, reco::GenParticleRef bQuark)
{ 
    double cosTheta = bQuark->p4().Vect().Dot( muon.momentum() ); 
    if( bQuark->p() != 0 )cosTheta = cosTheta /( bQuark->p() * muon.p() );// cos(theta)
    return std::sqrt(1 - cosTheta *cosTheta) * muon.p() ;// p * sin(theta) = pt
}

double GeneralUtilities::ptVsJetaxis( reco::Track muon , edm::Ref<edm::View<pat::Jet> > jetchosen  )
{
    
    double cosTheta = jetchosen->p4().Vect().Dot( muon.momentum() );
    if( jetchosen->p() != 0 )cosTheta = cosTheta / (jetchosen->p()*  muon.p()  );// cos(theta)
    return  std::sqrt(1 - cosTheta *cosTheta) * muon.p() ;// p * sin(theta) = pt

}
double GeneralUtilities::ptVsJetaxis(const reco::Candidate& muon, const reco::Candidate*& bQuark){

    double cosTheta = bQuark->p4().Vect().Dot( muon.momentum() ); 
    if( bQuark->p() != 0 )cosTheta = cosTheta /( bQuark->p() * muon.p() );// cos(theta)
    return std::sqrt(1 - cosTheta *cosTheta) * muon.p() ;// p * sin(theta) = pt

}
double GeneralUtilities::plVsJetaxis( reco::Track muon ,  const pat::JetRef  jetchosen  )
{
    
  double pl_muonjet = jetchosen->p4().Vect().Dot( muon.momentum() );
  if( jetchosen->p() != 0 )pl_muonjet = pl_muonjet / jetchosen->p();
  return pl_muonjet;
}
double GeneralUtilities::plVsJetaxis( reco::Track muon ,  const pat::Jet &  jetchosen  )
{
    
  double pl_muonjet = jetchosen.p4().Vect().Dot( muon.momentum() );
  if( jetchosen.p() != 0 )pl_muonjet = pl_muonjet / jetchosen.p();
  return pl_muonjet;
}
double GeneralUtilities::plVsJetaxis( const reco::GenParticleRef muon ,  const reco::GenParticleRef  bQuark)
{
    
  double pl_muonjet = bQuark->p4().Vect().Dot( muon->momentum() );
  if( bQuark->p() != 0 )pl_muonjet = pl_muonjet / bQuark->p();
  return pl_muonjet;
}
double GeneralUtilities::plVsJetaxis(const reco::Candidate& muon, reco::GenParticleRef bQuark)
{   
  double pl_muonjet = bQuark->p4().Vect().Dot( muon.momentum() );
  if( bQuark->p() != 0 )pl_muonjet = pl_muonjet / bQuark->p();
  return pl_muonjet;
}
double GeneralUtilities::plVsJetaxis( reco::Track muon , edm::Ref<edm::View<pat::Jet> > jetchosen  )
{
    
  double pl_muonjet = jetchosen->p4().Vect().Dot( muon.momentum() );
  if( jetchosen->p() != 0 )pl_muonjet = pl_muonjet / jetchosen->p();
  return pl_muonjet;
}
double GeneralUtilities::plVsJetaxis(const reco::Candidate& muon, const reco::Candidate*& bQuark){

  double pl_muonjet = bQuark->p4().Vect().Dot( muon.momentum() );
  if( bQuark->p() != 0 )pl_muonjet = pl_muonjet / bQuark->p();
  return pl_muonjet;

}
