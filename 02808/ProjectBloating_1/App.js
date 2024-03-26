import { StatusBar } from 'expo-status-bar';
import React, { useState } from 'react';
import { StyleSheet, View, Text, TouchableOpacity } from 'react-native';
import { LineChart } from 'react-native-chart-kit';

export default function App() {
  const [selectedMonth, setSelectedMonth] = useState(null);

  const data = {
    labels: ['January', 'February', 'March', 'April', 'May', 'June'],
    datasets: [
      {
        data: [20, 45, 28, 80, 99, 43],
        color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
        strokeWidth: 2
      }
    ]
  };

  const filteredData = {
    labels: data.labels,
    datasets: [
      {
        data: selectedMonth ? [data.datasets[0].data[selectedMonth]] : data.datasets[0].data,
        color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
        strokeWidth: 2
      }
    ]
  };

  return (
    <View style={styles.container}>
      <LineChart
        data={selectedMonth ? filteredData : data}
        width={350}
        height={220}
        yAxisLabel={'$'}
        chartConfig={{
          backgroundColor: '#e26a00',
          backgroundGradientFrom: '#fb8c00',
          backgroundGradientTo: '#ffa726',
          decimalPlaces: 2,
          color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
          style: {
            borderRadius: 16
          }
        }}
        bezier
        style={{
          marginVertical: 8,
          borderRadius: 16
        }}
      />
      <View style={styles.buttonsContainer}>
        {data.labels.map((label, index) => (
          <TouchableOpacity
            key={index}
            style={[styles.button, selectedMonth === index && styles.selectedButton]}
            onPress={() => setSelectedMonth(index)}>
            <Text style={styles.buttonText}>{label}</Text>
          </TouchableOpacity>
        ))}
        <TouchableOpacity
          style={[styles.button, !selectedMonth && styles.selectedButton]}
          onPress={() => setSelectedMonth(null)}>
          <Text style={styles.buttonText}>All Months</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center'
  },
  buttonsContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 20
  },
  button: {
    paddingHorizontal: 15,
    paddingVertical: 10,
    marginHorizontal: 5,
    borderRadius: 5,
    borderWidth: 1,
    borderColor: '#007bff'
  },
  selectedButton: {
    backgroundColor: '#007bff'
  },
  buttonText: {
    color: '#007bff'
  }
});
