package com.example.impresora20;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.util.Log;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class MyService extends Service {

    public static final String CHANNEL_ID = "personal_notifications";
    public static final int NOTIFICATION_ID = 001;
    public Handler timerHandler = new Handler();
    public boolean shouldRun = false;
    public Runnable timerRunnable = new Runnable() {
        @Override
        public void run() {
            if (shouldRun) {
                new connect().execute("bla");
                timerHandler.postDelayed(this, 5000);
            }
        }
    };

    @Override
    public int onStartCommand(Intent intent, int flags, int startId){
        timerRunnable.run();
        return super.onStartCommand(intent, flags, startId);
    }

    @Override
    public void onDestroy() {
        // STOP YOUR TASKS
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent){
        return null;
    }

    //Conecta no servidor
    class connect extends AsyncTask<String, Void, String> {

        public String x;
        public String y;

        public Exception exception;

        protected String doInBackground(String... urls ) {
            HttpURLConnection connection = null;
            try{
                URL url = new URL("http://192.168.0.101:8080/%C3%81rea%20de%20Trabalho/priorities.json");

                connection = (HttpURLConnection) url.openConnection();

                connection.setRequestProperty("Content-Type", "application/json");
                connection.setRequestProperty("Accept", "application/json");
                connection.setRequestProperty("Accept-Charset", "utf-8,*");
//                connection.setRequestMethod("POST");
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
                        boolean shouldRun = false;
                    }
                } finally {
                    connection.disconnect();
                }
            } catch (Exception e) {
                Log.e("ERROR", e.getMessage(), e);
            }
            return null;
        }

        protected void onPostExecute(MainActivity.connect feed) {
            // TODO: check this.exception
            // TODO: do something with the feed
        }
    }

    //Cria a notificação
    public void display(){

        creatNotificationChannel();
        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this, CHANNEL_ID);

        notificationBuilder.setSmallIcon(R.mipmap.baby_icon)
                .setContentTitle("A impressão acabou")
                .setContentText("Corre!!!")
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
