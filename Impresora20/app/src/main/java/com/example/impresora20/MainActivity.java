package com.example.impresora20;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {
    //Link of the stream video
    public String url ="http://189.29.17.149:9090";

    //Vriáveis de notificação
    public static final String CHANNEL_ID = "personal_notifications";
    public static final int NOTIFICATION_ID = 001;

    //test of loop
    public Handler timerHandler = new Handler();
    public boolean shouldRun = false;
    public Runnable timerRunnable = new Runnable() {
        @Override
        public void run() {
            if (shouldRun) {
                new connect().execute("bla");
                timerHandler.postDelayed(this, 1000);
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        timerRunnable.run();

        Button stream = (Button) findViewById(R.id.stream);
        Button start = (Button) findViewById(R.id.start);
        Button stop = (Button) findViewById(R.id.stop);

        final TextView estado = (TextView) findViewById(R.id.estado);

        stream.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                openUrl(url);
                sendTextNotification("Loading...");
            }
        });

        start.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendTextNotification("Start of monitoring");
                estado.setText("ON");
                shouldRun = true;
                timerRunnable.run();
            }
        });

        stop.setOnClickListener(new Button.OnClickListener() {
            @Override
            public void onClick(View view) {
                sendTextNotification("Monitoring cancellation");
                estado.setText("OFF");
                shouldRun = false;
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();

    }

    @Override
    protected void onPause() {
        super.onPause();
        timerRunnable.run();
    }


    @Override
    protected void onRestart() {
        super.onRestart();
        timerRunnable.run();
    }


    @Override
    protected void onResume() {
        super.onResume();
        timerRunnable.run();
    }


    @Override
    protected void onStart() {
        super.onStart();
        timerRunnable.run();
    }

    @Override
    protected void onStop() {
        super.onStop();
        timerRunnable.run();
    }



    //Button reaction
    private void sendTextNotification(String txt){
        Toast.makeText(getApplicationContext(), txt ,Toast.LENGTH_LONG).show();
    }

    //Open an URL
    public void openUrl(String url){
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.setData(Uri.parse(url));
        startActivity(intent);
    }

    //Connects to the server
    class connect extends AsyncTask<String, Void, String> {

        public String x;
        public String y;

        public Exception exception;

        protected String doInBackground(String... urls ) {
            HttpURLConnection connection = null;
            try{
                // Hear you put the alldres of your server
                URL url = new URL("http://192.168.0.101:8080/%C3%81rea%20de%20Trabalho/priorities.json");

                connection = (HttpURLConnection) url.openConnection();

                connection.setRequestProperty("Content-Type", "application/json");
                connection.setRequestProperty("Accept", "application/json");
                connection.setRequestProperty("Accept-Charset", "utf-8,*");
                //connection.setRequestMethod("POST");
                Log.d("Get-Request", url.toString());
                System.out.println(connection.getErrorStream());


                try {
                    BufferedReader bufferedReader = new BufferedReader(
                            new InputStreamReader(connection.getInputStream()));
                    StringBuilder stringBuilder = new StringBuilder();
                    String line;
                    while ((line = bufferedReader.readLine()) != null) {
                        stringBuilder.append(line).append("\n");
                    }
                    bufferedReader.close();
                    Log.d("Get-Response", stringBuilder.toString());
                    JSONObject json = new JSONObject(stringBuilder.toString());
                    System.out.print("Testando o json: ");
                    System.out.println(json);
                    System.out.println(json.get("estado"));
                    x= (String) json.get("estado");
                    y =(String) json.get("codigo");
                    if(new String("desligado").equals(x) && new String("ligado").equals(y) ){
                        display();
                        shouldRun = false;
                    }
                } finally {
                    connection.disconnect();
                }
            } catch (Exception e) {
                Log.e("ERROR", e.getMessage(), e);
            }
            return null;
        }

        protected void onPostExecute(connect feed) {
            // TODO: check this.exception
            // TODO: do something with the feed
        }
    }

    //Creates a nottification
    public void display(){

        creatNotificationChannel();
        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this, CHANNEL_ID);

        notificationBuilder.setSmallIcon(R.mipmap.baby_icon)
                .setContentTitle("The impression is ready")
                .setContentText("Run!!!")
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

        NotificationManagerCompat notificationManagerCompat = NotificationManagerCompat.from(this);
        notificationManagerCompat.notify(NOTIFICATION_ID,notificationBuilder.build());
    }

    public void creatNotificationChannel() {

        if (Build.VERSION.SDK_INT>=Build.VERSION_CODES.O){

            CharSequence name = "Personal Notification";
            String description = "Include all the pessonal notifications";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;

            NotificationChannel notificationChanel= new NotificationChannel(CHANNEL_ID, name,importance);

            notificationChanel.setDescription(description);

            NotificationManager notificationManager =(NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            notificationManager.createNotificationChannel(notificationChanel);
        }

    }


}

