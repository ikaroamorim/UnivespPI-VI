package com.example.pi_7_sem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.os.Bundle;
import android.widget.Spinner;
import android.widget.Toast;

import com.google.firebase.FirebaseError;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

import com.example.pi_7_sem.dados;
import com.google.firebase.database.ValueEventListener;
import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.util.ArrayList;

public class MainActivity extends AppCompatActivity {


dados data= new dados();
DatabaseReference referencia = FirebaseDatabase.getInstance().getReference().child("dados");

ArrayList<String> listCategoria = new ArrayList<String>();
ArrayList<String> listValor = new ArrayList<String>();
double[] vetor= new double[1000];
String aaa;




    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


       GraphView graph = (GraphView) findViewById(R.id.graph);

        LineGraphSeries<DataPoint> serie = new LineGraphSeries< >(new DataPoint[] {

                new DataPoint(0, 0),
                new DataPoint(2, 40),
                new DataPoint(3,20),
                new DataPoint(5,60),
                new DataPoint(6,40),
                new DataPoint(8,80)


        });
        graph.addSeries(serie);


        Button botao = (Button) findViewById(R.id.botao);
        botao.setOnClickListener(view -> {

        Spinner spinner1 = (Spinner)findViewById(R.id.spinner1);
        String textSpinner = spinner1.getSelectedItem().toString();
        int intSpinner= spinner1.getSelectedItemPosition();

        EditText compra = (EditText) findViewById(R.id.compra);

        EditText campoPreco = (EditText) findViewById(R.id.preco);
        double preco= Double.parseDouble(campoPreco.getText().toString());


        TextView resultado = (TextView)findViewById(R.id.resultado);


        data.setCompra(compra.getText().toString().trim());
        data.setCategoria(intSpinner);
        data.setValor(preco);

        referencia.push().setValue(data);



        referencia.addValueEventListener(new ValueEventListener(){
           @Override
           public void onDataChange(DataSnapshot dataSnapshot) {


               for (DataSnapshot ds: dataSnapshot.getChildren()){

                   listCategoria.add(ds.child("categoria").getValue().toString());
                   listValor.add(ds.child("valor").getValue().toString());
                   aaa=ds.child("valor").getValue().toString();

               }



           }

                @Override
                public void onCancelled(@NonNull DatabaseError error) {

                }


           });


            int m=0;

            for( int k=0; k<listCategoria.size();k++){

                if(Integer.parseInt(listCategoria.get(k)) == intSpinner){

                   vetor[k]=Double.parseDouble(listValor.get(m));
                   m=m+1;
                }
            }


         resultado.setText("Obrigado!");

         Toast.makeText(getApplicationContext(), "Dados salvos com sucesso!", Toast.LENGTH_SHORT).show();
         Toast.makeText(getApplicationContext(), referencia.child("dados").toString(), Toast.LENGTH_SHORT).show();


        });


    }
}