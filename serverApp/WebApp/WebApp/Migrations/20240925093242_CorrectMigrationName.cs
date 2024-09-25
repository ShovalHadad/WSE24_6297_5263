using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace WebApp.Migrations
{
    /// <inheritdoc />
    public partial class CorrectMigrationName : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Flights_FrequentFlyers_FrequentFlyerFlyerId",
                table: "Flights");

            migrationBuilder.DropForeignKey(
                name: "FK_Flights_Planes_PlaneId",
                table: "Flights");

            migrationBuilder.DropForeignKey(
                name: "FK_FlightTickets_Flights_FlightId",
                table: "FlightTickets");

            migrationBuilder.DropIndex(
                name: "IX_FlightTickets_FlightId",
                table: "FlightTickets");

            migrationBuilder.DropIndex(
                name: "IX_Flights_FrequentFlyerFlyerId",
                table: "Flights");

            migrationBuilder.DropIndex(
                name: "IX_Flights_PlaneId",
                table: "Flights");

            migrationBuilder.DropColumn(
                name: "FrequentFlyerFlyerId",
                table: "Flights");

            migrationBuilder.AlterColumn<int>(
                name: "PhoneNumber",
                table: "FrequentFlyers",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<string>(
                name: "Email",
                table: "FrequentFlyers",
                type: "nvarchar(max)",
                nullable: true,
                oldClrType: typeof(string),
                oldType: "nvarchar(max)");

            migrationBuilder.AddColumn<int>(
                name: "UserId",
                table: "FlightTickets",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats3",
                table: "Flights",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats2",
                table: "Flights",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats1",
                table: "Flights",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.AddColumn<int>(
                name: "FlyerId",
                table: "Flights",
                type: "int",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateIndex(
                name: "IX_Flights_FlyerId",
                table: "Flights",
                column: "FlyerId");

            migrationBuilder.AddForeignKey(
                name: "FK_Flights_FrequentFlyers_FlyerId",
                table: "Flights",
                column: "FlyerId",
                principalTable: "FrequentFlyers",
                principalColumn: "FlyerId",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Flights_FrequentFlyers_FlyerId",
                table: "Flights");

            migrationBuilder.DropIndex(
                name: "IX_Flights_FlyerId",
                table: "Flights");

            migrationBuilder.DropColumn(
                name: "UserId",
                table: "FlightTickets");

            migrationBuilder.DropColumn(
                name: "FlyerId",
                table: "Flights");

            migrationBuilder.AlterColumn<int>(
                name: "PhoneNumber",
                table: "FrequentFlyers",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<string>(
                name: "Email",
                table: "FrequentFlyers",
                type: "nvarchar(max)",
                nullable: false,
                defaultValue: "",
                oldClrType: typeof(string),
                oldType: "nvarchar(max)",
                oldNullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats3",
                table: "Flights",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats2",
                table: "Flights",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AlterColumn<int>(
                name: "NumOfTakenSeats1",
                table: "Flights",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.AddColumn<int>(
                name: "FrequentFlyerFlyerId",
                table: "Flights",
                type: "int",
                nullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_FlightTickets_FlightId",
                table: "FlightTickets",
                column: "FlightId");

            migrationBuilder.CreateIndex(
                name: "IX_Flights_FrequentFlyerFlyerId",
                table: "Flights",
                column: "FrequentFlyerFlyerId");

            migrationBuilder.CreateIndex(
                name: "IX_Flights_PlaneId",
                table: "Flights",
                column: "PlaneId");

            migrationBuilder.AddForeignKey(
                name: "FK_Flights_FrequentFlyers_FrequentFlyerFlyerId",
                table: "Flights",
                column: "FrequentFlyerFlyerId",
                principalTable: "FrequentFlyers",
                principalColumn: "FlyerId");

            migrationBuilder.AddForeignKey(
                name: "FK_Flights_Planes_PlaneId",
                table: "Flights",
                column: "PlaneId",
                principalTable: "Planes",
                principalColumn: "PlaneId",
                onDelete: ReferentialAction.Cascade);

            migrationBuilder.AddForeignKey(
                name: "FK_FlightTickets_Flights_FlightId",
                table: "FlightTickets",
                column: "FlightId",
                principalTable: "Flights",
                principalColumn: "FlightId",
                onDelete: ReferentialAction.Cascade);
        }
    }
}
