*.png")
        
        # Step 4, 5, 6: Count objects and generate CSV
        frames = sorted(glob.glob("/root/keyframes_*.png"))
        
        csv_path = "/root/counting_results.csv"
        with open(csv_path, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["frame_id", "coins", "enemies", "turtles"])
            
            for frame in frames:
                coins = count_objects_via_script(frame, "/root/coin.png")
                enemies = count_objects_via_script(frame, "/root/enemy.png")
                turt