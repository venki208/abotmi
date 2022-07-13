import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.Enumeration;
import java.util.ArrayList;
import java.security.cert.*;
import java.security.KeyStore;
import java.security.PrivateKey;
import java.security.Security;
import org.bouncycastle.cms.CMSProcessableByteArray;
import org.bouncycastle.cms.CMSSignedData;
import org.bouncycastle.cms.CMSSignedDataGenerator;
import org.bouncycastle.util.encoders.Base64;

public class pkcs7gen {
	public static void main(String args[]) throws Exception {
		if(args.length < 3) {
			System.exit(1);
		}
		KeyStore keystore = KeyStore.getInstance("jks");
		InputStream input = new FileInputStream(args[0]);
		try {
			char[] password=args[1].toCharArray();
			keystore.load(input, password);
		} catch (IOException e) {
		} finally {
		}
		Enumeration e = keystore.aliases();
		String alias = "";
		if(e!=null)
		{
			while (e.hasMoreElements())
			{
				String n = (String)e.nextElement();
				if (keystore.isKeyEntry(n))
				{
					alias = n;
				}
			}
		}
		PrivateKey privateKey=(PrivateKey) keystore.getKey(alias, args[1].toCharArray());
		X509Certificate myPubCert=(X509Certificate) keystore.getCertificate(alias);
		String dtos = args[2];
		byte[] dataToSign=dtos.getBytes();
		CMSSignedDataGenerator sgen = new CMSSignedDataGenerator();
		Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider ());
		sgen.addSigner(privateKey, myPubCert,CMSSignedDataGenerator.DIGEST_SHA1);
		Certificate[] certChain =keystore.getCertificateChain(alias);
		ArrayList certList = new ArrayList();
		for (int i=0; i < certChain.length; i++){
			certList.add(certChain[i]);
		}
		sgen.addCertificatesAndCRLs(CertStore.getInstance("Collection", new CollectionCertStoreParameters(certList), "BC"));
		CMSSignedData csd = sgen.generate(new CMSProcessableByteArray(dataToSign),true, "BC");
		
		byte[] signedData = csd.getEncoded();
		byte[] signedData64 = Base64.encode(signedData); 
		System.out.println(new String(signedData64));
	}	
}

